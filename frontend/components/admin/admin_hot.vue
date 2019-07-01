<template>
    <a-table :columns="columns" :dataSource="data">
        <span slot="action" slot-scope="text, record">
            <a href="javascript:;">编辑</a>
            <a-divider type="vertical" />
            <a href="javascript:;">删除</a>
            <a-divider type="vertical" />
        </span>
    </a-table>
</template>

<script>
import qs from 'qs'

export default {
  props: [],
  data() {
    return {
        columns: [{
            dataIndex: 'title',
            key: 'title'
        }, {
            title: '操作',
            key: 'action',
            scopedSlots: { customRender: 'action' }
        }]
    }
  },
  methods: {
  }
}
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>
