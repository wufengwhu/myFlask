from flask import Flask, Response, request, jsonify, json
from flask.ext.cors import CORS

from db import mogoClient
from db import mysqlClient

app = Flask(__name__)

CORS(app)

iblogDB = mogoClient.client.get_database('iBlog2')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


#
# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code"""
#
#     if isinstance(obj, date):
#         serial = obj.isoformat()
#         return serial
#     raise TypeError ("Type not serializable")

@app.route('/api/flow/<int:id>')
def getFlowConfigInfoById(id):
    # get flow config info by the id
    sql = "select id,description,DATE_FORMAT(updt_time, '%s') updt_time from FLOW_ACTION where `id` = %s" % (
        '%m-%d-%Y', id)
    res = mysqlClient.query(sql)[0]

    return jsonify(id=res['id'], updt_time=res['updt_time'], desc=res['description'])

    # return json.dumps(res)


# Blog Restful Service
# 分类列表
@app.route('/api/blog', methods=['POST', 'GET'], defaults={'category': None})
@app.route('/api/blog/<category>', methods=['POST'])
def get_category_list(category):
    categoryList = []
    if category is None:
        categoryList = [cate for cate in iblogDB.category.find()]
    else:
        categoryList = [cate for cate in iblogDB.category.find({"CateName": str(category)})]
    # if content is not None:
    #     content['']
    # TODO get data from mogodb
    return Response(json.dumps(categoryList), mimetype='application/json')


# 为首页数据查询构建条件对象
def getPostsQuery(params):
    query = {
        "IsActive": True,
        "IsDraft": False}
    filterType = {
        '1': "Title",
        '2': "Labels",
        '3': "CreateTime"
    }
    if params.get("cateId") is not None:
        query["CategoryId"] = params["cateId"]
    if params.get('keyword') != '' and not None:
        condition = filterType.get(params['filterType'], "$or")
        if condition != "$or":
            query[condition] = {"$regex": params['keyword'], "$options": "i"}
        else:
            query[condition] = [{
                "Title": {
                    "$regex": params['keyword'],
                    "$options": "i"
                }
            }, {
                'Labels': {
                    "$regex": params['keyword'],
                    "$options": "i"
                }
            }, {
                'Summary': {
                    "$regex": params['keyword'],
                    "$options": "i"
                }
            }, {
                'Content': {
                    "$regex": params['keyword'],
                    "$options": "i"
                }
            }]
    return query


# 获取首页的文章数据
@app.route('/api/blog/getPosts', methods=['POST', 'GET'])
def get_posts():
    content = request.get_json(silent=True)
    page = int(content.get('pageIndex', 1))
    size = int(content.get('pgeSize', 10))
    page = page > 0 and page or 1
    skip = (page - 1) * size
    limit = size
    sort = content.get('sortBy', 'title') == 'Title' and 'Title -CreateTime' or '-CreateTime'
    query = getPostsQuery(content)
    posts = [post for post in iblogDB.post.find(query).skip(skip).sort(sort)]
    count = iblogDB.post.count(query)
    pageCount = count % size == 0 and int(count / size) or int(count / size) + 1

    return jsonify(posts=posts, pageCount=pageCount)

    #return Response(json.dumps({"posts": posts, "pageCount": pageCount}), mimetype='application/json')


if __name__ == '__main__':
    app.run()
