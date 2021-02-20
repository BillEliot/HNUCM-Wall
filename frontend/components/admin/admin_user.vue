<template>
    <div>
        <!-- drawer -->
        <a-drawer
            title="编辑用户信息"
            :width="360"
            @close="visible = false"
            :visible="visible"
            :wrapStyle="{ height: 'calc(100% - 108px)', overflow: 'auto', paddingBottom: '108px' }"
        >
            <a-form :form="form" layout="vertical">
                <a-form-item label="uid">
                    <a-input v-decorator="['uid']" disabled />
                </a-form-item>
                <a-form-item label="email">
                    <a-input
                        v-decorator="['email', {
                            rules: [{
                                type: 'email', message: '请输入有效的EMail',
                            }, {
                                required: true, message: '请输入EMail',
                            }]
                        }]"
                        placeholder="输入email"
                    />
                </a-form-item>
                <a-form-item label="昵称">
                    <a-input
                        v-decorator="['username', {
                            rules: [{ required: true, message: '请输入昵称', whitespace: true }]
                        }]"
                        placeholder="输入昵称"
                    />
                </a-form-item>
                <a-form-item label="个性签名">
                    <a-input
                        v-decorator="['bio', {
                            rules: [{ required: true, message: '请输入个性签名', whitespace: true }]
                        }]"
                        placeholder="输入个性签名"
                    />
                </a-form-item>
                <a-form-item label="班级">
                    <a-cascader
                        v-decorator="['class',{
                                initialValue: ['zhongyi', 'wuyi'],
                                rules: [{ type: 'array', required: true, message: '请选择您的班级' }],
                            }
                        ]"
                        :options="classes"
                    />
                </a-form-item>
                <a-form-item label="手机">
                    <a-input
                        v-decorator="['phone', {
                            rules: [{
                                validator: validator_phone
                            }]
                        }]"
                        placeholder="输入手机"
                        type="number"
                    />
                </a-form-item>
                <a-form-item label="qq">
                    <a-input
                        v-decorator="['qq']"
                        placeholder="输入qq"
                        type="number"
                    />
                </a-form-item>
                <a-form-item label="微信">
                    <a-input
                        v-decorator="['wechat']"
                        placeholder="输入微信"
                    />
                </a-form-item>
                <a-form-item label="硬币">
                    <a-input
                        v-decorator="['coin']"
                        placeholder="输入硬币"
                        type="number"
                    />
                </a-form-item>
                <a-form-item label="管理员">
                    <a-switch
                        v-decorator="['isAdmin', { 
                            valuePropName: 'checked' 
                        }]"
                    />
                </a-form-item>
                <a-form-item label="身份认证(用;分隔)">
                    <a-input
                        v-decorator="['auth']"
                        placeholder="输入身份认证"
                    />
                </a-form-item>
            </a-form>
            <div
                :style="{
                    position: 'absolute',
                    left: 0,
                    bottom: 0,
                    width: '100%',
                    borderTop: '1px solid #e9e9e9',
                    padding: '10px 16px',
                    background: '#fff',
                    textAlign: 'right',
                }"
            >
                <a-button
                    :style="{ marginRight: '8px' }"
                    @click="visible = false"
                >
                    取消
                </a-button>
                <a-button @click="updateUserAdmin" type="primary">确定</a-button>
            </div>
        </a-drawer>
        <!-- end -->
        <a-table :columns="columns" :dataSource="userList">
            <a slot="username" slot-scope="text">{{ text }}</a>
            <span slot="isAdmin" slot-scope="isAdmin">
                <a-tag v-if="isAdmin == true" color="green">是</a-tag>
                <a-tag v-else color="red">否</a-tag>
            </span>
            <span slot="action" slot-scope="text, record">
                <a @click="update(record.key)">编辑</a>
                <a-divider type="vertical" />
                <a-popconfirm title="确定删除？" @confirm="deleteUser(record.key)" okText="确定" cancelText="取消">
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
    </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  data() {
    return {
        visible: false,
        form: this.$form.createForm(this),
        userList: [],
        columns: [{
            dataIndex: 'key',
            title: 'id',
            key: 'key'
        }, {
            dataIndex: 'email',
            title: 'EMail',
        }, {
            dataIndex: 'username',
            title: '昵称',
            scopedSlots: { customRender: 'username' }
        }, {
            dataIndex: 'bio',
            title: '个性签名',
        }, {
            dataIndex: 'class',
            title: '班级',
        }, {
            dataIndex: 'phone',
            title: '手机',
        }, {
            dataIndex: 'qq',
            title: 'qq',
        }, {
            dataIndex: 'wechat',
            title: '微信',
        }, {
            dataIndex: 'coin',
            title: '硬币',
        }, {
            dataIndex: 'isAdmin',
            title: '管理员',
            scopedSlots: { customRender: 'isAdmin' },
        }, {
            dataIndex: 'auth',
            title: '身份认证',
        }, {
            title: '操作',
            scopedSlots: { customRender: 'action' }
        }]
    }
  },
  methods: {
      validator_phone (rule, value, callback) {
          var regex_phone = /^1[34578]\d{9}$/
          if (value && !regex_phone.test(value)) {
              callback('请输入合法的手机号')
          }
          callback()
      },
      refresh() {
          this.$axios.get('getUserList')
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.userList = res.data.info
              }
          })
      },
      update(id) {
          this.visible = true
          this.$axios.post('getUserDetail', qs.stringify({
              uid: id
          }))
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.form.setFieldsValue({
                      uid: id,
                      email: res.data.email,
                      username: res.data.username,
                      bio: res.data.bio,
                      class: res.data.class,
                      phone: res.data.phone,
                      qq: res.data.qq,
                      wechat: res.data.wechat,
                      coin: res.data.coin,
                      isAdmin: res.data.isAdmin,
                      auth: res.data.auth
                  })
              }
          })
          this.visible = true
      },
      updateUserAdmin(e) {
          e.preventDefault()
          this.form.validateFieldsAndScroll((err, values) => {
              if (!err) {
                  this.$axios.post('updateUserAdmin', qs.stringify({
                      uid: values.id,
                      email: values.email,
                      username: values.username,
                      bio: values.bio,
                      class: values.class,
                      phone: values.phone,
                      qq: values.qq,
                      wechat: values.wechat,
                      coin: values.coin,
                      isAdmin: values.isAdmin,
                      auth: values.auth
                  }))
                  .then((res) => {
                      if (res.data == 0) {
                          this.$message.success('操作成功')
                          this.form.resetFields()
                          this.visible = false
                          this.refresh()
                      }
                      else if (res.data == 1) {
                          this.$message.error('未知错误')
                      }
                  })
              }
          })
      },
      deleteUser(id) {
          this.$axios.post('deleteUser', qs.stringify({
              id: id
          }))
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.$message.success('删除成功')
                  let userList = [...this.userList]
                  this.userList = userList.filter(item => item.key !== id)
              }
          })
      }
  },
  mounted() {
      this.refresh()
  },
  computed: mapState({
    classes: state => state.classes,
  })
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.action {
    margin: 10px 10px
}
</style>
