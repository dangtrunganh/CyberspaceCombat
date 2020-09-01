# import os
# print(os.path.abspath(os.path.dirname(__file__)))
# print(os.path.dirname(__file__))
# print(os.pardir)
#
# print(os.path.join(os.path.dirname(__file__), 'static', 'upload_file'))


labels = [1, 2, 3]
x_ = [2, 3, 1]

import matplotlib.pyplot as plt
plt.ylabel('number of posts')
plt.xlabel('number of users')
plt.plot(labels, x_)
plt.show()
# plt.savefig('./sdkh.png')
