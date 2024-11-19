import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const signUp = function (payload) {
    // const username = payload.username
    // const password1 = payload.password1
    // const password2 = payload.password2
    const { username, password1, password_confirm,emill } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password_confirm,emill
      }
    })
      .then((res) => {
        // console.log(res)
        // console.log('회원가입 성공')
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const logIn = function (payload) {
    // const username = payload.username
    // const password1 = payload.password
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.key
        router.push({ name: 'ArticleView' })
        // console.log(res.data)
        // console.log('로그인 성공')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const writes = ref([{id : 1,title:'가나다',content:'글내용'},
    {id : 2,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
    {id : 3,title:'가나다',content:'글내용'},
  ])

  const fowllers = ref([{name:'가나다',count:1},
    {name:'나가다',count:12},
    {name:'다나다',count:13},
    {name:'다나다',count:13},
    {name:'다나다',count:13},
  ])

  const moive = ref([
    {img :'https://picsum.photos/200/30',title:'1번',content :'줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다'},
    {img :'https://picsum.photos/200/30',title:'1번',content :'줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다'},
    {img :'https://picsum.photos/200/30',title:'1번',content :'줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다'},
    {img :'https://picsum.photos/200/30',title:'1번',content :'줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다'},
    {img :'https://picsum.photos/200/30',title:'1번',content :'줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다'},
    {img :'https://picsum.photos/200/30',title:'1번',content :'줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다'},
    {img :'https://picsum.photos/200/30',title:'1번',content :'줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다줄거리입니다'},

  ])
  return { signUp,logIn,writes,fowllers,moive}
}, {persist : true})
