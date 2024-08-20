class AppRoutes:
    def __init__(self, app, user_auth, zpl_label_designer):
        self.app = app
        self.user_auth = user_auth
        self.zpl_label_designer = zpl_label_designer
        self.add_routes()

    def add_routes(self):
        self.app.add_url_rule("/sign_up", methods=["POST"], view_func=self.user_auth.sign_up)
        self.app.add_url_rule("/sign_in", methods=["POST"], view_func=self.user_auth.sign_in)
        self.app.add_url_rule("/sign_out", methods=["POST"], view_func=self.user_auth.sign_out)
        self.app.add_url_rule("/token_refresh", methods=["POST"], view_func=self.user_auth.token_refresh)
        self.app.add_url_rule("/all_users", methods=["POST"], view_func=self.user_auth.get_all_users)
        self.app.add_url_rule("/update_user", methods=["PUT"], view_func=self.user_auth.update_user)
        self.app.add_url_rule("/delete_user", methods=["DELETE"], view_func=self.user_auth.delete_user)
        self.app.add_url_rule("/generate_zpl", methods=["POST"], view_func=self.zpl_label_designer.generate_zpl)
        self.app.add_url_rule("/print_thermal_label", methods=["POST"], view_func=self.zpl_label_designer.print_thermal_label)