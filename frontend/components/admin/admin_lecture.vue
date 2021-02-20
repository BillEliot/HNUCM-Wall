<template>
    <div>
        <!-- drawer -->
        <a-drawer
            title="添加讲座动态"
            placement="top"
            height=512
            @close="cancelDrawer"
            :visible="visible"
        >
            <a-form :form="form" layout="vertical">
                <a-form-item label="id">
                    <a-input
                        v-decorator="['id', {
                            initialValue: -1
                        }]"
                        disabled
                    />
                </a-form-item>
                <a-form-item label="标题">
                    <a-input
                        v-decorator="['title', {
                            rules: [{ required: true, message: '请输入标题' }]
                        }]"
                        placeholder="输入标题"
                    />
                </a-form-item>
                <a-form-item label="嘉宾">
                    <a-input
                        v-decorator="['lecturer', {
                            rules: [{ required: true, message: '请输入嘉宾姓名' }]
                        }]"
                        placeholder="输入嘉宾姓名"
                    />
                </a-form-item>
                <a-form-item label="嘉宾信息">
                    <markdown_editor
                        v-decorator="['lecturerInfo', {
                            rules: [{ required: true, message: '请输入嘉宾信息' }],
                            initialValue: ''
                        }]"
                        style="z-index: 0"
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
                <a-form-item label="讲座时间">
                    <a-range-picker
                        v-decorator="['date', {
                            rules: [{ required: true, message: '请输入讲座时间' }]
                        }]"
                        format="YYYY-MM-DD HH:mm:ss"
                        :showTime="true"
                        style="width: 50%"
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
                    @click="cancelDrawer"
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
        <a-table :columns="columns" :dataSource="lectureList" rowKey="id">
            <span slot="date" slot-scope="date">{{ moment(date).format('YYYY-MM-DD HH:mm:ss') }}</span>
            <span slot="action" slot-scope="text, record">
                <a @click="update(record.id)">编辑</a>
                <a-divider type="vertical" />
                <a-popconfirm title="确定删除？" @confirm="deleteLecture(record.id)" okText="确定" cancelText="取消">
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
    </div>
</template>

<script>
import qs from 'qs'
import markdown_editor from '@/components/markdown_editor.vue'
import moment from 'moment'

export default {
  components: {
      markdown_editor
  },
  data() {
    return {
        moment,

        visible: false,
        form: this.$form.createForm(this),
        lectureList: [],
        columns: [{
            dataIndex: 'id',
            title: 'id',
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
            dataIndex: 'startDate',
            title: '开始时间',
        }, {
            dataIndex: 'endDate',
            title: '结束时间',
        }, {
            dataIndex: 'state',
            title: '状态'
        }, {
            title: '操作',
            scopedSlots: { customRender: 'action' }
        }]
    }
  },
  async fetch() {
      this.refresh()
  },
  methods: {
      disabledDate(current) {
        return current < moment().subtract(1, 'days').endOf('day')
      },
      disabledDateTime() {
        return {
        }
      },
      refresh() {
          this.$axios.get('getLectureList')
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.lectureList = response.data.data
              }
          })
      },
      update(id) {
          this.$axios.get('getLectureDetail', {
              params: {
                  id: id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.form.setFieldsValue({
                      id: id,
                      title: response.data.data.title,
                      lecturer: response.data.data.lecturer,
                      lecturerInfo: response.data.data.lecturerInfo,
                      address: response.data.data.address,
                      date: [
                          moment(response.data.data.startDate, 'YYYY-MM-DD HH:mm:ss'),
                          moment(response.data.data.endDate, 'YYYY-MM-DD HH:mm:ss')
                      ]
                  })
              }
          })
          this.visible = true
      },
      cancelDrawer() {
          this.form.resetFields()
          this.visible = false
      },
      addLecture(e) {
          e.preventDefault()
          this.form.validateFieldsAndScroll((err, values) => {
              if (!err) {
                  this.$axios.post('addLecture', qs.stringify({
                      id: values.id,
                      title: values.title,
                      lecturer: values.lecturer,
                      lecturerInfo: values.lecturerInfo,
                      address: values.address,
                      startDate: values.date[0].format("YYYY-MM-DD HH:mm:ss"),
                      endDate: values.date[1].format("YYYY-MM-DD HH:mm:ss")
                  }))
                  .then((response) => {
                      if (response.data.code == 200 && response.data.status == 'success') {
                          this.$message.success('操作成功')
                          this.form.resetFields()
                          this.visible = false
                          this.refresh()
                      }
                  })
              }
          })
      },

      deleteLecture(id) {
          this.$axios.get('deleteLecture', {
              params: {
                  id: id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
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
