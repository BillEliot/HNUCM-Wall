export default function ({ $axios, redirect }) {
    $axios.get('getUserBaseInfo')
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            if (response.data.data.id == -1) {
                redirect('/login')
            }
        }
    })
}
 