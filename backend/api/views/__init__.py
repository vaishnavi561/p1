from .auth import RegisterView, login_view, setup_2fa_view, verify_and_enable_2fa_view, forgot_password_view, reset_password_confirm_view
from .profiles import family_profile_list_create, family_profile_detail
from .chat import ai_chat_view,model_health_check
from .scan import scan_prescription_view