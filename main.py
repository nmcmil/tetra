import sys
import os
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('WebKit', '6.0')

from gi.repository import Gtk, Adw, WebKit, Gio, Gdk, GLib

class TetraWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Tetra")
        self.set_default_size(1200, 800)

        # Main Layout Container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)
        
        # Single Global Header Bar
        self.header_bar = Adw.HeaderBar()
        self.header_bar.set_title_widget(Gtk.Label(label="Tetra", css_classes=["title"]))
        
        # Collapse Button (Hamburger)
        self.collapse_btn = Gtk.Button(icon_name="view-sidebar-symbolic")
        self.collapse_btn.set_tooltip_text("Toggle Sidebar")
        self.collapse_btn.connect("clicked", self.on_collapse_clicked)
        self.header_bar.pack_start(self.collapse_btn)
        
        main_box.append(self.header_bar)
        
        # Split View (Below Header)
        self.split_view = Adw.OverlaySplitView()
        self.split_view.set_sidebar_position(Gtk.PackType.START)
        self.split_view.set_vexpand(True) # Expand to fill rest of window
        
        # Sidebar Content
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.add_css_class("background") 
        
        # List Box
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.list_box.add_css_class("navigation-sidebar")
        self.list_box.connect("row-selected", self.on_row_selected)
        
        sidebar_scroll = Gtk.ScrolledWindow()
        sidebar_scroll.set_child(self.list_box)
        sidebar_scroll.set_vexpand(True)
        sidebar_box.append(sidebar_scroll)
        
        self.split_view.set_sidebar(sidebar_box)

        # Content Area
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # No content header anymore
        
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        
        content_box.append(self.stack)
        self.split_view.set_content(content_box)
        
        main_box.append(self.split_view)
        
        # Add Breakpoint for Mobile
        breakpoint = Adw.Breakpoint.new(Adw.BreakpointCondition.parse("max-width: 800px"))
        breakpoint.add_setter(self.split_view, "collapsed", True)
        self.add_breakpoint(breakpoint)

        # Base path for assets
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Add Services
        self.services = [
            {"id": "chatgpt", "name": "ChatGPT", "url": "https://chatgpt.com", "icon_file": os.path.join(self.base_dir, "assets/chatgpt.png")},
            {"id": "grok", "name": "Grok", "url": "https://x.com/i/grok", "icon_file": os.path.join(self.base_dir, "assets/grok.png")},
            {"id": "gemini", "name": "Gemini", "url": "https://gemini.google.com", "icon_file": os.path.join(self.base_dir, "assets/gemini.png")},
            {"id": "claude", "name": "Claude", "url": "https://claude.ai", "icon_file": os.path.join(self.base_dir, "assets/claude.png")},
        ]


        # Persistence Setup
        data_dir = os.path.join(GLib.get_user_data_dir(), "tetra")
        cache_dir = os.path.join(GLib.get_user_cache_dir(), "tetra")
        
        # Ensure directories exist
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(cache_dir, exist_ok=True)
        
        # Create persistent session
        self.network_session = WebKit.NetworkSession.new(data_dir, cache_dir)

        for service in self.services:
            # Add to Sidebar
            row = Gtk.ListBoxRow()
            row.add_css_class("sidebar-row")
            row.service_id = service["id"]
            
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            
            label = Gtk.Label(label=service["name"], xalign=0)
            label.add_css_class("sidebar-label")
            
            row_box.append(label)
            row.set_child(row_box)
            self.list_box.append(row)
            
            # Add WebView to Stack
            # Share the persistent session across all views
            webview = WebKit.WebView(network_session=self.network_session)
            webview.set_vexpand(True)
            webview.set_hexpand(True)
            settings = webview.get_settings()
            settings.set_enable_developer_extras(True)
            settings.set_enable_javascript(True)
            settings.set_enable_media_stream(True) # Enable camera/mic access for voice features
            
            self.stack.add_named(webview, service["id"])
            
            # Initial load
            webview.load_uri(service["url"])

        # Select first item
        self.list_box.select_row(self.list_box.get_row_at_index(0))

    def on_collapse_clicked(self, btn):
        # Toggle sidebar visibility
        current = self.split_view.get_show_sidebar()
        self.split_view.set_show_sidebar(not current)

    def on_row_selected(self, box, row):
        if row:
            self.stack.set_visible_child_name(row.service_id)
            
            # On mobile (collapsed), hide sidebar after selection
            if self.split_view.get_collapsed():
                self.split_view.set_show_sidebar(False)

class TetraApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.ubuntu.tetra",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = TetraWindow(self)
        
        # Load CSS
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, "style.css")
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(css_path)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        win.present()

if __name__ == "__main__":
    GLib.set_prgname("com.ubuntu.tetra")
    GLib.set_application_name("Tetra")
    app = TetraApp()
    app.run(sys.argv)
