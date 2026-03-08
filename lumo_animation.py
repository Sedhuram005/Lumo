import tkinter as tk
import threading
import time

def show_animation():
    """Show glowing Lumo animation window"""
    root = tk.Tk()
    root.title("Lumo Assistant")
    root.geometry("300x200")
    root.configure(bg="black")
    
    # Center window on screen
    root.eval('tk::PlaceWindow . center')
    
    label = tk.Label(
        root,
        text="LUMO",
        fg="cyan",
        bg="black",
        font=("Arial", 32, "bold")
    )
    
    label.pack(expand=True)
    
    # Glowing pulse animation
    def animate():
        size = 32
        grow = True
        
        for _ in range(20):  # Animate for 2 seconds
            if grow:
                size += 2
            else:
                size -= 2
            
            if size >= 50:
                grow = False
            if size <= 30:
                grow = True
            
            # Change color for glow effect
            if size >= 40:
                color = "#00ffff"  # Bright cyan
            elif size >= 35:
                color = "#00cccc"  # Light cyan
            else:
                color = "cyan"
            
            label.config(font=("Arial", size, "bold"), fg=color)
            root.update()
            time.sleep(0.05)
        
        # Close after animation
        root.after(2000, root.destroy)
    
    # Start animation in separate thread
    animation_thread = threading.Thread(target=animate, daemon=True)
    animation_thread.start()
    
    root.mainloop()

def show_wake_animation():
    """Quick wake animation - just pulse once"""
    root = tk.Tk()
    root.title("Lumo Active")
    root.geometry("300x150")
    root.configure(bg="black")
    root.eval('tk::PlaceWindow . center')
    
    label = tk.Label(
        root,
        text="LUMO",
        fg="#00ffff",  # Bright cyan
        bg="black",
        font=("Arial", 36, "bold")
    )
    
    label.pack(expand=True)
    
    # Single pulse effect
    for size in range(32, 45, 3):
        label.config(font=("Arial", size, "bold"))
        root.update()
        time.sleep(0.03)
    
    root.after(500, root.destroy)

if __name__ == "__main__":
    show_animation()
