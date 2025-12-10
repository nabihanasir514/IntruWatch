# Event linked list for Campus Guardian system
class EventNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class EventLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
        self.max_size = 5  # Keep last 5 events

    def add_event(self, event_data):
        new_node = EventNode(event_data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

        # Trim old events if size exceeds max_size
        if self.size > self.max_size:
            current = self.head
            for _ in range(self.max_size - 1):
                current = current.next
            current.next = None
            self.size = self.max_size

    def get_all_events(self):
        events = []
        current = self.head
        while current:
            events.append(current.data)
            current = current.next
        return events

if __name__ == "__main__":
    event_log = EventLinkedList()

    # Add realistic campus intrusion/security events
    event_log.add_event("Gate 1 Breach Detected")
    event_log.add_event("Unauthorized Access in Lab 3")
    event_log.add_event("Motion Detected Near Library")
    event_log.add_event("Fire Alarm Triggered in Cafeteria")
    event_log.add_event("Suspicious Person in Parking Lot")
    event_log.add_event("Emergency Exit Door Forced Open")  # Oldest event will be trimmed

    # Display recent security events (newest to oldest)
    print("Recent Campus Security Events:")
    for event in event_log.get_all_events():
        print(event)
