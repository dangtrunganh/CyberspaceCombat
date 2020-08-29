# -*- coding: utf-8 -*-

from nlp_core import PoliticClassification
pc = PoliticClassification()

content = '''donald trump,trump,tập cận bình,đảng dân chủ của việt nam đã sang một trang hoàn toàn mới
trung quốc,zalo,hotline,freeship,ship,liên hệ,inbox,ib,giải_thưởng, bill,free,xin việc,mail
chạy chức,chạy quyền,bằng_cấp giả,lạm_dụng chức_quyền'''
x_clean, x_result = pc.predict_single_post(content)

print(x_clean)
print(x_result)
# print(x_clean)
# print(x_predict[0])
# print(prob)
