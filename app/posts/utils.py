def get_post_image_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / ...
    return f"blogs/posts/{filename}"
