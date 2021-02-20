<template>
    <div>
        <!-- drawer -->
        <a-drawer
            title="添加校园热点"
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
                <a-form-item label="类型">
                    <a-select
                        v-decorator="['type', {
                            rules: [{ required: true, message: '请选择类型' }],
                            initialValue: '新闻'
                        }]"
                        placeholder="选择类型"
                    >
                        <a-select-option value="新闻">新闻</a-select-option>
                        <a-select-option value="通知">通知</a-select-option>
                        <a-select-option value="招标公告">招标公告</a-select-option>
                        <a-select-option value="中标公告">中标公告</a-select-option>
                        <a-select-option value="瓜">瓜</a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item label="内容">
                    <markdown_editor
                        v-decorator="['content', {
                            rules: [{ required: true, message: '请输入内容' }],
                            initialValue: ''
                        }]"
                        style="z-index: 0"
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
                <a-button @click="addHot" type="primary">确定</a-button>
            </div>
        </a-drawer>
        <!-- end -->
        <div class="action">
            <a-button type="primary" @click="visible = true">添加</a-button>
        </div>
        <a-table :columns="columns" :dataSource="hotList" rowKey="id">
            <a-tag slot="type" slot-scope="text">{{ text }}</a-tag>
            <span slot="action" slot-scope="text, record">
                <a @click="update(record.id)">编辑</a>
                <a-divider type="vertical" />
                <a-popconfirm title="确定删除？" @confirm="deleteHot(record.id)" okText="确定" cancelText="取消">
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
    </div>
</template>

<script>
import qs from 'qs'
import markdown_editor from '@/components/markdown_editor.vue'

export default {
  components: {
      markdown_editor
  },
  data() {
    return {
        visible: false,
        form: this.$form.createForm(this),
        hotList: [],
        columns: [{
            dataIndex: 'id',
            title: 'id',
        }, {
            dataIndex: 'title',
            title: '标题',
        }, {
            dataIndex: '_type',
            title: '类型',
            scopedSlots: { customRender: 'type' }
        }, {
            dataIndex: 'date',
            title: '日期',
        }, {
            title: '操作',
            scopedSlots: { customRender: 'action' }
        }],
    }
  },
  async fetch() {
      this.refresh()
  },
  methods: {
      refresh() {
          this.$axios.get('getHotList')
          .then((response) => {
              this.hotList = response.data.data
          })
      },
      update(id) {
          this.$axios.get('getHotDetail', {
              params: {
                  id: id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.form.setFieldsValue({
                      id: response.data.data.id,
                      title: response.data.data.title,
                      type: response.data.data.type,
                      content: response.data.data.content
                  })
              }
          })
          this.visible = true
      },
      cancelDrawer() {
          this.form.resetFields()
          this.visible = false
      },
      addHot(e) {
          e.preventDefault()
          this.form.validateFieldsAndScroll((err, values) => {
              if (!err) {
                  this.$axios.post('addHot', qs.stringify({
                      id: values.id,
                      title: values.title,
                      type: values.type,
                      content: values.content
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
      deleteHot(id) {
          this.$axios.get('deleteHot', {
              params: {
                  id: id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.$message.success('删除成功')
                  let hotList = [...this.hotList]
                  this.hotList = hotList.filter(item => item.id !== id)
              }
          })
      },
      $imgAdd(pos, $file) {
          var formdata = new FormData()
          formdata.append('image', $file)
          this.$axios({
              url: 'uploadImg_JinGui',
              method: 'post',
              data: formdata,
              headers: { 'Content-Type': 'multipart/form-data' },
          })
          .then((response) => {
              this.$refs.md.$img2Url(pos, this.baseUrl + '/media/img/JinGui/' + response.data)
              this.cover = response.data
          })
      },
      $imgDel(url) {
          this.$axios.post('removeImg_JinGui', qs.stringify({
              url: url[0]
          }))
          .then((response) => {
              if (response.data == 0) {
                  this.$message.success('删除成功')
              }
              else {
                  this.$message.error('未知错误')
              }
          })
      }
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
