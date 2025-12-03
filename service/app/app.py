# app.py
"""시리얼 모니터 애플리케이션"""

import threading
import time
from typing import Dict
from queue import Queue

from database import DatabaseHandler
from monitor import SerialMonitor
from queue_processor import QueueProcessor


class SerialMonitorApp:
    """시리얼 모니터 애플리케이션"""
    
    def __init__(self, db_config: dict, port_config: dict):
        self.db_handler = DatabaseHandler(**db_config)
        self.port_config = port_config
        self.cmd_queue = Queue()
        self.monitors: Dict[str, SerialMonitor] = {}
        self.threads = []
        self.queue_processor = None
    
    def start(self) -> bool:
        """애플리케이션 시작"""
        print("=" * 60)
        print("시리얼 모니터 시작")
        print("=" * 60)
        
        # DB 연결
        if not self.db_handler.connect():
            return False
        
        # 포트 연결
        self._setup_monitors()
        if not self.monitors:
            print("[✗] 연결된 포트가 없습니다")
            self.db_handler.close()
            return False
        
        # 모니터 스레드 시작
        self._start_monitor_threads()
        
        # 큐 처리 스레드 시작
        self._start_queue_processor()
        
        print(f"\n[✓] {len(self.monitors)}개 포트 모니터링 중\n")
        return True
    
    def _setup_monitors(self):
        """모니터 설정"""
        for device_id, port in self.port_config.items():
            monitor = SerialMonitor(device_id, port, self.cmd_queue, self.db_handler)
            monitor.available_devices = list(self.port_config.keys())
            if monitor.connect():
                self.monitors[device_id] = monitor
    
    def _start_monitor_threads(self):
        """모니터 스레드 시작"""
        for device_id, monitor in self.monitors.items():
            thread = threading.Thread(
                target=monitor.run,
                daemon=True,
                name=f"Monitor-{device_id}"
            )
            thread.start()
            self.threads.append(thread)
    
    def _start_queue_processor(self):
        """큐 처리 스레드 시작"""
        self.queue_processor = QueueProcessor(self.cmd_queue, self.monitors)
        
        # 모든 monitor에 queue_processor 할당 (ACK 처리용)
        for monitor in self.monitors.values():
            monitor.queue_processor = self.queue_processor
        
        thread = threading.Thread(
            target=self.queue_processor.run,
            daemon=True,
            name="QueueProcessor"
        )
        thread.start()
        self.threads.append(thread)
    
    def stop(self):
        """애플리케이션 종료"""
        print("\n" + "=" * 60)
        print("종료 중...")
        print("=" * 60)
        
        if self.queue_processor:
            self.queue_processor.stop()
        
        for monitor in self.monitors.values():
            monitor.close()
        
        self.db_handler.close()
        
        for thread in self.threads:
            thread.join(timeout=1)
        
        print("[✓] 모든 리소스 종료 완료")
    
    def run(self):
        """메인 루프"""
        if not self.start():
            return
        
        try:
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\nCtrl+C로 종료...")
        
        finally:
            self.stop()