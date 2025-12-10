import heapq
from datetime import datetime
import time

# 4. Priority Queue (Heap) for Alerts (Campus Guardian System)
class AlertSystem:
    def __init__(self):
        # Heap to store alerts as tuples: (priority, timestamp, message)
        # Python heapq is a min-heap → smallest priority (1 = High) comes first
        self.heap = []
        # Priority map:
        # 1 = High (Immediate threat, e.g., Fire, Intrusion)
        # 2 = Medium (Suspicious activity, e.g., motion near camera)
        # 3 = Low (Minor alerts, e.g., low battery, system warning)
    
    def add_alert(self, priority, message):
        """
        Adds a new alert to the system with current timestamp.
        Arguments:
            priority: int → 1 (High), 2 (Medium), 3 (Low)
            message: str → description of the alert
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        heapq.heappush(self.heap, (priority, timestamp, message))
    
    def get_active_alerts(self):
        """
        Returns a sorted list of all active alerts.
        Sorting order: priority → timestamp
        (Does NOT remove alerts from the heap)
        """
        return sorted(self.heap)


# ===== Example Usage (Campus Guardian Alerts) =====
if __name__ == "__main__":
    alert_system = AlertSystem()
    
    # Adding alerts related to camera/security and general safety
    alert_system.add_alert(2, "Motion Detected near Gate 1 Camera")       # Medium priority
    time.sleep(1)
    alert_system.add_alert(1, "Intrusion Detected in Lab 3")             # High priority
    time.sleep(1)
    alert_system.add_alert(1, "Fire Alarm Triggered in Cafeteria")       # High priority
    time.sleep(1)
    alert_system.add_alert(3, "Camera 2 Battery Low")                    # Low priority
    time.sleep(1)
    alert_system.add_alert(2, "Unauthorized Access Attempt at Library")  # Medium priority
    time.sleep(1)
    alert_system.add_alert(3, "System Maintenance Reminder")             # Low priority
    
    # Get all active alerts sorted by priority (High → Medium → Low)
    active_alerts = alert_system.get_active_alerts()
    
    print("Active Campus Guardian Alerts (sorted by priority):")
    for alert in active_alerts:
        print(f"Priority: {alert[0]}, Time: {alert[1]}, Message: {alert[2]}")
