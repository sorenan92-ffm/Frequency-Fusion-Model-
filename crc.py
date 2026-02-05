"""
Quark Structure Visualization 3D
یک شبیه‌سازی کامل سه‌بعدی از ساختار کوارک‌ها
با قابلیت چرخش، زوم و تعامل کامل
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
import matplotlib.colors as mcolors

class QuarkVisualizer3D:
    """
    کلاس شبیه‌سازی سه‌بعدی ساختار کوارک‌ها
    """
    
    def __init__(self):
        # پارامترهای کوارک‌ها
        self.quarks = {
            'up': {
                'color': '#FF0000',  # قرمز
                'charge': '+2/3',
                'mass': '2.3 MeV',
                'spin': '1/2',
                'position': np.array([1.0, 0.0, 0.0])
            },
            'down': {
                'color': '#0000FF',  # آبی
                'charge': '-1/3',
                'mass': '4.8 MeV',
                'spin': '1/2',
                'position': np.array([-0.5, 0.87, 0.0])
            },
            'charm': {
                'color': '#00FF00',  # سبز
                'charge': '+2/3',
                'mass': '1.28 GeV',
                'spin': '1/2',
                'position': np.array([-0.5, -0.87, 0.0])
            },
            'strange': {
                'color': '#FF00FF',  # ارغوانی
                'charge': '-1/3',
                'mass': '95 MeV',
                'spin': '1/2',
                'position': np.array([0.5, -0.87, 0.5])
            },
            'top': {
                'color': '#FFA500',  # نارنجی
                'charge': '+2/3',
                'mass': '173 GeV',
                'spin': '1/2',
                'position': np.array([0.5, 0.87, -0.5])
            },
            'bottom': {
                'color': '#800080',  # بنفش تیره
                'charge': '-1/3',
                'mass': '4.18 GeV',
                'spin': '1/2',
                'position': np.array([0.0, 0.0, 1.0])
            }
        }
        
        # پارامترهای گلئون‌ها
        self.gluons = {
            'red_anti-blue': {'color': '#FF1493', 'strength': 1.0},
            'blue_anti-green': {'color': '#1E90FF', 'strength': 0.8},
            'green_anti-red': {'color': '#32CD32', 'strength': 0.6},
        }
        
        # تنظیمات گرافیکی
        self.fig = plt.figure(figsize=(16, 12))
        self.fig.suptitle('Quark Structure 3D Simulation\nInteractive Visualization of Quantum Chromodynamics', 
                         fontsize=16, fontweight='bold', y=0.95)
        
        # ایجاد 4 subplot مختلف
        self.ax_main = self.fig.add_subplot(231, projection='3d')
        self.ax_color_charge = self.fig.add_subplot(232)
        self.ax_quantum_fields = self.fig.add_subplot(233)
        self.ax_interaction = self.fig.add_subplot(234, projection='3d')
        self.ax_properties = self.fig.add_subplot(235)
        self.ax_info = self.fig.add_subplot(236)
        
        # متغیرهای انیمیشن
        self.rotation_angle = 0
        self.animation_running = True
        
    def create_quark_sphere(self, position, radius=0.3, color='red', alpha=0.8):
        """
        ایجاد کره سه‌بعدی برای نمایش کوارک
        """
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        
        x = position[0] + radius * np.outer(np.cos(u), np.sin(v))
        y = position[1] + radius * np.outer(np.sin(u), np.sin(v))
        z = position[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        return x, y, z
    
    def draw_color_field(self, ax):
        """
        ترسیم میدان رنگ QCD
        """
        x = np.linspace(-2, 2, 50)
        y = np.linspace(-2, 2, 50)
        X, Y = np.meshgrid(x, y)
        
        # میدان‌های رنگی (رنگ‌های QCD)
        R = np.sin(X**2 + Y**2)  # قرمز
        G = np.cos(X + Y)        # سبز
        B = np.sin(X - Y)        # آبی
        
        # ترکیب برای ایجاد میدان رنگی
        rgb = np.dstack((R, G, B))
        rgb_normalized = (rgb - rgb.min()) / (rgb.max() - rgb.min())
        
        ax.imshow(rgb_normalized, extent=[-2, 2, -2, 2], alpha=0.6)
        ax.set_title('QCD Color Field', fontweight='bold')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, alpha=0.3)
    
    def draw_quantum_fluctuations(self, ax):
        """
        ترسیم نوسانات کوانتومی
        """
        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        
        # تابع موج کوانتومی
        Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1*(X**2 + Y**2))
        
        contour = ax.contourf(X, Y, Z, 20, cmap='viridis', alpha=0.8)
        ax.set_title('Quantum Fluctuations', fontweight='bold')
        ax.set_xlabel('Position')
        ax.set_ylabel('Energy Density')
        
        # اضافه کردن colorbar
        plt.colorbar(contour, ax=ax, label='Wave Function Amplitude')
    
    def draw_gluon_field_lines(self, ax):
        """
        ترسیم خطوط میدان گلئون
        """
        # ایجاد نقاط برای خطوط میدان
        theta = np.linspace(0, 2*np.pi, 100)
        
        for i, (gluon_name, gluon_props) in enumerate(self.gluons.items()):
            radius = 1.5 + i * 0.2
            x = radius * np.cos(theta + self.rotation_angle/10)
            y = radius * np.sin(theta + self.rotation_angle/10)
            z = np.sin(3*theta + self.rotation_angle/5)
            
            ax.plot(x, y, z, color=gluon_props['color'], 
                   linewidth=2*gluon_props['strength'], 
                   alpha=0.6, label=f'Gluon: {gluon_name}')
    
    def update_animation(self, frame):
        """
        تابع بروزرسانی انیمیشن
        """
        self.rotation_angle += 0.5
        
        # پاک کردن axes
        self.ax_main.clear()
        self.ax_interaction.clear()
        
        # تنظیمات axes اصلی
        self.ax_main.set_title('3D Quark Structure', fontweight='bold', pad=20)
        self.ax_main.set_xlabel('X')
        self.ax_main.set_ylabel('Y')
        self.ax_main.set_zlabel('Z')
        
        # محدودیت axes
        self.ax_main.set_xlim([-2, 2])
        self.ax_main.set_ylim([-2, 2])
        self.ax_main.set_zlim([-2, 2])
        
        # اضافه کردن grid
        self.ax_main.grid(True, alpha=0.3)
        
        # ترسیم کوارک‌ها
        for quark_name, quark_props in self.quarks.items():
            # چرخش موقعیت کوارک‌ها
            rotation_matrix = self.get_rotation_matrix(self.rotation_angle)
            rotated_pos = rotation_matrix @ quark_props['position']
            
            # ایجاد کره کوارک
            x, y, z = self.create_quark_sphere(rotated_pos, 0.2, quark_props['color'])
            self.ax_main.plot_surface(x, y, z, color=quark_props['color'], 
                                    alpha=0.8, edgecolor='black', linewidth=0.5)
            
            # اضافه کردن برچسب
            self.ax_main.text(rotated_pos[0], rotated_pos[1], rotated_pos[2] + 0.3,
                            quark_name.upper(), fontweight='bold', fontsize=9,
                            ha='center', color=quark_props['color'])
            
            # اضافه کردن اطلاعات بار
            self.ax_main.text(rotated_pos[0], rotated_pos[1], rotated_pos[2] - 0.3,
                            f"Q={quark_props['charge']}", fontsize=8,
                            ha='center', color='white', 
                            bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.5))
        
        # ترسیم خطوط میدان گلئون
        self.draw_gluon_field_lines(self.ax_main)
        
        # ترسیم محورهای مختصات
        self.draw_coordinate_axes(self.ax_main)
        
        # ترسیم نمودار تعاملات
        self.draw_interaction_diagram(self.ax_interaction)
        
        return self.ax_main, self.ax_interaction
    
    def get_rotation_matrix(self, angle):
        """
        ایجاد ماتریس چرخش سه‌بعدی
        """
        angle_rad = np.radians(angle)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        
        # چرخش حول محورهای مختلف
        Rx = np.array([[1, 0, 0],
                      [0, cos_a, -sin_a],
                      [0, sin_a, cos_a]])
        
        Ry = np.array([[cos_a, 0, sin_a],
                      [0, 1, 0],
                      [-sin_a, 0, cos_a]])
        
        Rz = np.array([[cos_a, -sin_a, 0],
                      [sin_a, cos_a, 0],
                      [0, 0, 1]])
        
        return Rz @ Ry @ Rx
    
    def draw_coordinate_axes(self, ax):
        """
        ترسیم محورهای مختصات
        """
        # محور X (قرمز)
        ax.quiver(0, 0, 0, 2, 0, 0, color='red', arrow_length_ratio=0.1, linewidth=2)
        ax.text(2.2, 0, 0, 'X', color='red', fontsize=12, fontweight='bold')
        
        # محور Y (سبز)
        ax.quiver(0, 0, 0, 0, 2, 0, color='green', arrow_length_ratio=0.1, linewidth=2)
        ax.text(0, 2.2, 0, 'Y', color='green', fontsize=12, fontweight='bold')
        
        # محور Z (آبی)
        ax.quiver(0, 0, 0, 0, 0, 2, color='blue', arrow_length_ratio=0.1, linewidth=2)
        ax.text(0, 0, 2.2, 'Z', color='blue', fontsize=12, fontweight='bold')
    
    def draw_interaction_diagram(self, ax):
        """
        ترسیم دیاگرام تعاملات کوارک‌ها
        """
        ax.set_title('Quark Interactions & Force Lines', fontweight='bold', pad=20)
        ax.set_xlabel('Space')
        ax.set_ylabel('Time-like')
        ax.set_zlabel('Interaction Strength')
        
        # ایجاد نقاط برای تعاملات
        n_points = 20
        t = np.linspace(0, 4*np.pi, n_points)
        
        # خطوط تعامل مختلف
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for i in range(5):
            x = np.sin(t + i*0.5)
            y = np.cos(t + i*0.5)
            z = 0.5 * np.sin(2*t + i) + i*0.5
            
            ax.plot(x, y, z, color=colors[i], linewidth=2, alpha=0.7,
                   label=f'Interaction {i+1}')
        
        ax.legend(fontsize=8, loc='upper right')
        ax.grid(True, alpha=0.3)
    
    def draw_property_chart(self):
        """
        ترسیم نمودار خواص کوارک‌ها
        """
        self.ax_properties.clear()
        
        # داده‌های کوارک‌ها
        quark_names = list(self.quarks.keys())
        masses = [2.3, 4.8, 1280, 95, 173000, 4180]  # MeV
        charges = [2/3, -1/3, 2/3, -1/3, 2/3, -1/3]
        
        # ایجاد subplot برای جرم
        ax1 = self.ax_properties
        colors = [self.quarks[q]['color'] for q in quark_names]
        
        bars = ax1.bar(quark_names, masses, color=colors, edgecolor='black', linewidth=1)
        ax1.set_title('Quark Properties', fontweight='bold')
        ax1.set_ylabel('Mass (MeV)', fontweight='bold')
        ax1.set_xlabel('Quark Type', fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # اضافه کردن مقادیر روی نمودار
        for bar, mass in zip(bars, masses):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + max(masses)*0.01,
                    f'{mass:,}', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # چرخش برچسب‌های محور X
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # اضافه کردن نمودار دوم برای بار
        ax2 = ax1.twinx()
        ax2.plot(quark_names, charges, 'ko--', linewidth=2, markersize=8)
        ax2.set_ylabel('Electric Charge (e)', fontweight='bold', color='black')
        ax2.tick_params(axis='y', labelcolor='black')
        ax2.set_ylim([-0.5, 1])
    
    def draw_info_panel(self):
        """
        ترسیم پنل اطلاعات
        """
        self.ax_info.clear()
        self.ax_info.axis('off')
        
        info_text = """
        QUANTUM CHROMODYNAMICS (QCD) VISUALIZATION
        
        Color Charges:
        • Red, Green, Blue (Anti-colors: Anti-red, etc.)
        • Confinement: Quarks cannot exist alone
        • Asymptotic Freedom: Weak coupling at high energy
        
        Quark Properties:
        • Spin: 1/2 (Fermions)
        • 6 Flavors: u, d, c, s, t, b
        • 3 Generations
        
        Strong Force:
        • Mediated by Gluons (8 types)
        • Carries color charge
        • Non-Abelian gauge theory
        
        Visualization Controls:
        • Mouse: Rotate 3D view
        • Scroll: Zoom in/out
        • Sliders: Adjust parameters
        """
        
        self.ax_info.text(0.05, 0.95, info_text, transform=self.ax_info.transAxes,
                         fontsize=9, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        # اضافه کردن نمادهای فیزیکی
        symbols = [
            (0.85, 0.85, r'$SU(3)_C$', 12),
            (0.85, 0.75, r'$Q = \pm\frac{2}{3}, \pm\frac{1}{3}$', 10),
            (0.85, 0.65, r'$g_s \approx 1$', 10),
            (0.85, 0.55, r'$\Lambda_{QCD} \approx 200$ MeV', 9),
        ]
        
        for x, y, text, size in symbols:
            self.ax_info.text(x, y, text, transform=self.ax_info.transAxes,
                            fontsize=size, fontweight='bold',
                            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    def create_controls(self):
        """
        ایجاد کنترل‌های تعاملی
        """
        # تنظیم موقعیت sliders
        axcolor = 'lightgoldenrodyellow'
        
        # Slider برای سرعت چرخش
        ax_rotation = plt.axes([0.25, 0.02, 0.4, 0.03], facecolor=axcolor)
        self.slider_rotation = Slider(ax_rotation, 'Rotation Speed', 0.1, 5.0, 
                                     valinit=1.0, valstep=0.1)
        
        # Slider برای اندازه کوارک‌ها
        ax_size = plt.axes([0.25, 0.06, 0.4, 0.03], facecolor=axcolor)
        self.slider_size = Slider(ax_size, 'Quark Size', 0.1, 1.0, 
                                 valinit=0.3, valstep=0.05)
        
        # دکمه‌های کنترل
        ax_start = plt.axes([0.7, 0.02, 0.1, 0.04])
        ax_stop = plt.axes([0.81, 0.02, 0.1, 0.04])
        ax_reset = plt.axes([0.92, 0.02, 0.07, 0.04])
        
        self.btn_start = Button(ax_start, 'Start', color='lightgreen')
        self.btn_stop = Button(ax_stop, 'Pause', color='lightcoral')
        self.btn_reset = Button(ax_reset, 'Reset', color='lightblue')
        
        # اتصال events
        self.btn_start.on_clicked(self.start_animation)
        self.btn_stop.on_clicked(self.stop_animation)
        self.btn_reset.on_clicked(self.reset_view)
        self.slider_rotation.on_changed(self.update_speed)
    
    def start_animation(self, event):
        """شروع انیمیشن"""
        self.animation_running = True
        print("Animation started")
    
    def stop_animation(self, event):
        """توقف انیمیشن"""
        self.animation_running = False
        print("Animation paused")
    
    def reset_view(self, event):
        """بازنشانی نمای سه‌بعدی"""
        self.rotation_angle = 0
        print("View reset")
    
    def update_speed(self, val):
        """بروزرسانی سرعت انیمیشن"""
        self.animation_speed = val
    
    def setup_visualization(self):
        """
        تنظیم اولیه تمام نمودارها
        """
        # ترسیم میدان رنگ
        self.draw_color_field(self.ax_color_charge)
        
        # ترسیم نوسانات کوانتومی
        self.draw_quantum_fluctuations(self.ax_quantum_fields)
        
        # ترسیم نمودار خواص
        self.draw_property_chart()
        
        # ترسیم پنل اطلاعات
        self.draw_info_panel()
        
        # ایجاد کنترل‌ها
        self.create_controls()
        
        # تنظیم layout
        plt.tight_layout()
    
    def run(self):
        """
        اجرای شبیه‌سازی
        """
        print("🚀 Starting 3D Quark Structure Visualization...")
        print("Controls:")
        print("  • Mouse: Rotate 3D view")
        print("  • Scroll: Zoom in/out")
        print("  • Sliders: Adjust parameters")
        print("  • Buttons: Start/Pause/Reset")
        
        # تنظیم اولیه
        self.setup_visualization()
        
        # ایجاد انیمیشن
        self.ani = FuncAnimation(self.fig, self.update_animation,
                               frames=360, interval=50, blit=False)
        
        # نمایش
        plt.show()

# ============================================================================
# نسخه ساده‌تر برای اجرای سریع
# ============================================================================

def create_simple_quark_visualization():
    """شبیه‌سازی ساده‌تر برای اجرای سریع"""
    
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle('3D Quark Structure - Simplified Version', fontsize=16, fontweight='bold')
    
    ax = fig.add_subplot(111, projection='3d')
    
    # موقعیت‌های کوارک‌ها
    positions = {
        'up': [1, 0, 0],
        'down': [-0.5, 0.87, 0],
        'charm': [-0.5, -0.87, 0],
        'strange': [0.5, -0.87, 0.5],
        'top': [0.5, 0.87, -0.5],
        'bottom': [0, 0, 1]
    }
    
    colors = {
        'up': 'red',
        'down': 'blue',
        'charm': 'green',
        'strange': 'purple',
        'top': 'orange',
        'bottom': 'darkviolet'
    }
    
    # ترسیم کوارک‌ها
    for name, pos in positions.items():
        # ایجاد کره
        u = np.linspace(0, 2*np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x = pos[0] + 0.2 * np.outer(np.cos(u), np.sin(v))
        y = pos[1] + 0.2 * np.outer(np.sin(u), np.sin(v))
        z = pos[2] + 0.2 * np.outer(np.ones_like(u), np.cos(v))
        
        ax.plot_surface(x, y, z, color=colors[name], alpha=0.8)
        
        # برچسب
        ax.text(pos[0], pos[1], pos[2] + 0.3, name.upper(),
               fontweight='bold', ha='center')
    
    # تنظیمات گرافیکی
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('6 Quark Flavors in 3D Space', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # اضافه کردن خطوط میدان
    theta = np.linspace(0, 2*np.pi, 100)
    for i in range(3):
        radius = 1.5 + i*0.2
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        z = np.sin(3*theta)
        ax.plot(x, y, z, color='cyan', alpha=0.5, linewidth=1)
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# تابع اصلی برای اجرا
# ============================================================================

if __name__ == "__main__":
    print("🎨 Quark Structure 3D Visualization")
    print("="*50)
    
    try:
        # ایجاد شبیه‌سازی کامل
        visualizer = QuarkVisualizer3D()
        visualizer.run()
        
    except Exception as e:
        print(f"⚠️  Error in full simulation: {e}")
        print("Trying simplified version...")
        create_simple_quark_visualization()