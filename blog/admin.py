from datetime import datetime, timedelta, timezone
from django.contrib import admin
from blog.models import Post

admin.site.register(Post)

# TODO IMPLEMENT ME
# from background_task import background
# @background(schedule=20)#timedelta(hours=24))
# def cleandbposts():
# 	now=datetime.now(timezone.utc)
# 	invalid=Post.objects.filter(definitive=False)
# 	for inv in invalid:
# 		if (now-inv.publish_date).hours>=1:
# 			inv.delete()

# cleandbposts()