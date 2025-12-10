from collections import deque

#  Queue for Camera Frames (FIFO)
class FrameQueue:
    def __init__(self, max_size=10):
        # Queue with a maximum size
        self.queue = deque(maxlen=max_size)

    def add_frame(self, frame_data):
        # Add a new frame to the queue
        self.queue.append(frame_data)
    
    def get_frame(self):
        # Get the oldest frame (FIFO)
        if self.queue:
            return self.queue.popleft()
        return None
    
    def peek(self):
        # See all frames without removing
        return list(self.queue)

if __name__ == "__main__":
    frame_queue = FrameQueue(max_size=3)
    
    # Add frames
    frame_queue.add_frame("Frame1")
    frame_queue.add_frame("Frame2")
    frame_queue.add_frame("Frame3")
    print("Current frames:", frame_queue.peek())
    
    # Add one more frame, oldest will be removed automatically
    frame_queue.add_frame("Frame4")
    print("After adding Frame4:", frame_queue.peek())
    
    # Get frames (FIFO)
    oldest_frame = frame_queue.get_frame()
    print("Processing oldest frame:", oldest_frame)
    print("Frames left in queue:", frame_queue.peek())
