"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.download_image import download_image
from insta485.views.user import show_user
from insta485.views.followers import show_followers
from insta485.views.following import show_following
from insta485.views.post import show_post
from insta485.views.login import login
from insta485.views.logout import logout
from insta485.views.accounts_create import accounts_create
from insta485.views.accounts import accounts
from insta485.views.accounts_delete import accounts_delete
from insta485.views.accounts_edit import accounts_edit
from insta485.views.accounts_password import accounts_password
from insta485.views.likes import likes
from insta485.views.comments import comments
from insta485.views.posts import posts
from insta485.views.follow import following
from insta485.views.explore import show_explore
