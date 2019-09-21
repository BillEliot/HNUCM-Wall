<template>
    <div>
        <!-- drawer -->
        <a-drawer
            title="添加讲座动态"
            :width="360"
            @close="visible = false"
            :visible="visible"
            :wrapStyle="{ height: 'calc(100% - 108px)',overflow: 'auto',paddingBottom: '108px' }"
        >
            <a-form :form="form" layout="vertical">
                <a-form-item label="标题">
                    <a-input
                        v-decorator="['title', {
                            rules: [{ required: true, message: '请输入标题' }]
                        }]"
                        placeholder="输入标题"
                    />
                </a-form-item>
                <a-form-item label="讲座人">
                    <a-input
                        v-decorator="['lecturer', {
                            rules: [{ required: true, message: '请输入讲座人' }]
                        }]"
                        placeholder="输入讲座人"
                    />
                </a-form-item>
                <a-form-item label="地址">
                    <a-input
                        v-decorator="['address', {
                            rules: [{ required: true, message: '请输入地址' }]
                        }]"
                        placeholder="输入地址"
                    />
                </a-form-item>
                <a-form-item label="讲座日期">
                    <a-date-picker
                        v-decorator="['date', {
                            rules: [{ required: true, message: '请输入讲座日期' }]
                        }]"
                        format="YYYY-MM-DD"
                        :disabledDate="disabledDate"
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
                <a-button @click="addLecture" type="primary">确定</a-button>
            </div>
        </a-drawer>
        <!-- end -->
        <div class="action">
            <a-button type="primary" @click="visible = true">添加</a-button>
        </div>
        <a-table :columns="columns" :dataSource="lectureList">
            <span slot="state" slot-scope="state">
                <a-tag v-if="state == 'wait'" color="red">未开始</a-tag>
                <a-tag v-if="state == 'running'" color="green">进行中</a-tag>
                <a-tag v-if="state == 'done'" color="gray">已结束</a-tag>
            </span>
            <span slot="action" slot-scope="text, record">
                <a @click="update(record.key)">编辑</a>
                <a-divider type="vertical" />
                <a-popconfirm title="确定删除？" @confirm="deleteLecture(record.key)" okText="确定" cancelText="取消">
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'

export default {
  data() {
    return {
        visible: false,
        form: this.$form.createForm(this),
        lectureList: [],
        columns: [{
            dataIndex: 'key',
            title: 'id',
            key: 'key'
        }, {
            dataIndex: 'title',
            title: '标题',
        }, {
            dataIndex: 'lecturer',
            title: '讲座人',
        }, {
            dataIndex: 'address',
            title: '地址',
        }, {
            dataIndex: 'date',
            title: '讲座日期',
        }, {
            dataIndex: 'state',
            title: '讲座状态',
            scopedSlots: { customRender: 'state' },
        }, {
            title: '操作',
            scopedSlots: { customRender: 'action' }
        }]
    }
  },
  methods: {
      disabledDate(current) {
        return current < moment().subtract(1, 'days').endOf('day')
      },
      refresh() {
          this.$axios.get('getLectureList')
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.lectureList = res.data.info
              }
          })
      },
      update(id) {
          this.$axios.post('getLectureDetail', qs.stringify({
              id: id
          }))
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.form.setFieldsValue({
                      title: res.data.title,
                      lecturer: res.data.lecturer,
                      address: res.data.address,
                      date: moment(res.data.date, 'YYYY-MM-DD')
                  })
              }
          })
          this.visible = true
      },
      addLecture(e) {
          e.preventDefault()
          this.form.validateFieldsAndScroll((err, values) => {
              if (!err) {
                  this.$axios.post('addLecture', qs.stringify({
                      title: values.title,
                      lecturer: values.lecturer,
                      address: values.address,
                      date: values.date.format("YYYY-MM-DD")
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
      deleteLecture(id) {
          this.$axios.post('deleteLecture', qs.stringify({
              id: id
          }))
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.$message.success('删除成功')
                  let lectureList = [...this.lectureList]
                  this.lectureList = lectureList.filter(item => item.key !== id)
              }
          })
      }
  },
  mounted() {
      this.refresh()
  }
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
