def get_blog_image_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / ...
    return 'blogs/{}-{}/images/{}'.format(instance.title,
                                          instance.author.user.username,
                                          filename)


def get_post_image_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / ...
    return 'blogs/{}-{}-{}/images/posts/{}'.format(instance.blog.title,
                                                   instance.blog.author.first_name,
                                                   instance.blog.author.last_name,
                                                   filename)
