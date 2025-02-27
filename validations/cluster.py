from .validation import validator

@validator.register("cluster")
def validate_cluster(value):
    # 您的验证逻辑
    if len(value) < 5:
        return "<div class='error'>集群名称至少需要5个字符</div>"
    return "<div class='success'>名称有效</div>"
