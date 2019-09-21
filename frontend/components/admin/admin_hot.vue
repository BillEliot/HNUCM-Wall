<template>
    <div>
        <!-- drawer -->
        <a-drawer
            title="添加校园热点"
            :width="720"
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
                <a-form-item label="内容(markdown)">
                    <a-textarea
                        v-decorator="['content', {
                            rules: [{ required: true, message: '请输入内容(markdown)' }]
                        }]"
                        placeholder="输入内容(markdown)" :rows="8"
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
                <a-button @click="addHot" type="primary">确定</a-button>
            </div>
        </a-drawer>
        <!-- end -->
        <div class="action">
            <a-button type="primary" @click="visible = true">添加</a-button>
        </div>
        <a-table :columns="columns" :dataSource="hotList">
            <a slot="publisher" slot-scope="publisher">{{ publisher.nickname }}</a>
            <span slot="action" slot-scope="text, record">
                <a @click="update(record.key)">编辑</a>
                <a-divider type="vertical" />
                <a-popconfirm title="确定删除？" @confirm="deleteHot(record.key)" okText="确定" cancelText="取消">
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
    </div>
</template>

<script>
import qs from 'qs'

export default {
  props: ['uid'],
  data() {
    return {
        visible: false,
        form: this.$form.createForm(this),
        hotList: [],
        columns: [{
            dataIndex: 'key',
            title: 'id',
            key: 'key'
        }, {
            dataIndex: 'title',
            title: '标题',
        }, {
            dataIndex: 'publisher',
            title: '发布者',
            scopedSlots: { customRender: 'publisher' }
        }, {
            dataIndex: 'date',
            title: '日期',
        }, {
            title: '操作',
            scopedSlots: { customRender: 'action' }
        }]
    }
  },
  methods: {
      refresh() {
          this.$axios.get('getHotList')
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.hotList = res.data.info
              }
          })
      },
      update(id) {
          this.$axios.post('getHotDetail', qs.stringify({
              id: id
          }))
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.form.setFieldsValue({
                      title: res.data.title,
                      content: res.data.content
                  })
              }
          })
          this.visible = true
      },
      addHot(e) {
          e.preventDefault()
          this.form.validateFieldsAndScroll((err, values) => {
              if (!err) {
                  this.$axios.post('addHot', qs.stringify({
                      title: values.title,
                      content: values.content,
                      publisherUID: this.uid
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
      deleteHot(id) {
          this.$axios.post('deleteHot', qs.stringify({
              id: id
          }))
          .then((res) => {
              if (res.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.$message.success('删除成功')
                  let hotList = [...this.hotList]
                  this.hotList = hotList.filter(item => item.key !== id)
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
