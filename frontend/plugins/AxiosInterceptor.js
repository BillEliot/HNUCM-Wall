import axios from 'axios'
import { message } from 'ant-design-vue/lib'

export default function ({ $axios, redirect, error }) {
    $axios.onResponse(response => {
        switch (response.data.code) {
            case 302:
                redirect(response.data.path)
                break
            case 400:
                error({ statusCode: 400, message: '非法请求' })
                break
            case 403:
                error({ statusCode: 400, message: '没有权限' })
                break
            case 500:
                error({ statusCode: 500, message: 'Server错误' })
                break
            case 200:
                if (response.data.status == 'error') {
                    message.error(response.data.message)
                }
                else if (response.data.status == 'warning') {
                    message.warning(response.data.message)
                }
                break
        }
    })
}
