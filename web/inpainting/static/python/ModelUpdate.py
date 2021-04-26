from Processing.models import Post

def insert_value(value):
    a=Post()
    a.rating=value
    a.save()

def select_value(id=-1):
    if id==-1:
        Post.objects.all()
    else:
        Post.objects.get(id=id)

def update_value(id,value):
    a = Post.objects.get(id=id)
    a.rating=value
    a.save()
