from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from datetime import datetime
from kivy.clock import Clock
from screens.login import PantallaLogin

# Solo se queda PantallaPrincipal aquí
class PantallaPrincipal(Screen):
    reloj_programado = False

    def on_enter(self):
        app = App.get_running_app()
        rol = getattr(app, "rol", "USUARIO").upper()
        terminal = getattr(app, "terminal", "N/A")
        dias = getattr(app, "dias_licencia", 0)

        mensajes = {
            "ADMINISTRADOR": (
                "Bienvenida Administradora de BoliBank SYSTEM.\n"
                "Tienes control total sobre el sistema."
            ),
            "LISTERO": (
                f"Hola Listero \nTerminal: {terminal} | Licencia activa por {dias} días.\n"
                "Estamos esperando tus jugadas."
            ),
            "RECOLECTOR": (
                f"Hola Recolector \nTerminal: {terminal} | Licencia activa por {dias} días.\n"
                "Listo para reunir las listas."
            ),
            "CABEZA DE BANCO": (
                f"Saludos Cabeza de Banco \nTerminal: {terminal} | Licencia activa por {dias} días.\n"
                "Toma el mando y lidera el banco."
            ),
            "BANCO": (
                f"Hola Banco \nTerminal: {terminal} | Licencia activa por {dias} días.\n"
                "Autoriza y supervisa las operaciones."
            ),
        }

        self.ids.mensaje_entrada.text = mensajes.get(
            rol, f"Bienvenido {rol}!\nTerminal: {terminal} | Licencia activa por {dias} días"
        )

        if not PantallaPrincipal.reloj_programado:
            Clock.schedule_interval(self.actualizar_reloj, 1)
            PantallaPrincipal.reloj_programado = True

        self.actualizar_reloj(0)

    def actualizar_reloj(self, dt):
        hora = datetime.now().strftime("%I:%M:%S %p")
        self.ids.reloj_label.text = f"{hora}"

class MiApp(App):
    title = "BoliBank SYSTEM"
    rol = "USUARIO"
    terminal = "N/A"
    dias_licencia = 0

    def simular_login(self, rol, terminal, dias):
        self.rol = rol.upper()
        self.terminal = terminal
        self.dias_licencia = dias

    def build(self):
        Builder.load_file("app.kv")
        sm = ScreenManager()
        # Asumimos que PantallaLogin se importa desde login.py o similar
        from screens.login import PantallaLogin
        sm.add_widget(PantallaLogin(name="login"))
        sm.add_widget(PantallaPrincipal(name="principal"))
        self.icon = "assets/icono_bolibank.png"
        return sm

if __name__ == "__main__":
    MiApp().run()

