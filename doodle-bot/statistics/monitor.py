

def total_objects(bucket):
    objs = [i for i in bucket.objects.all()]
    total = len(objs)

    return total
