def get_post_image_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / ...
    return 'blogs/{slug}/images/posts/{filename}'.format(
        slug=instance.section.post.slug,
        filename=filename
    )
