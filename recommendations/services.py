from posts.models import Post

def recommended_posts(user):

    language = user.profile.language

    posts = Post.objects.filter(language=language)

    return posts.order_by("-created_at")