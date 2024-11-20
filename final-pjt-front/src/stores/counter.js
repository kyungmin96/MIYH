import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'


export const useCounterStore = defineStore('counter', () => {
const API_URL = 'http://127.0.0.1:8000'
  const userKey=ref(null)
  const token = ref(null)
  const router = useRouter()
  const currentUser = ref(null)
  const events = ref(null)
  const fowllers =ref(null)

  const addOrUpdateEvent = (newEvent) => {
    const existingEventIndex = events.value.findIndex(event => event.start === newEvent.start)
    
    if (existingEventIndex !== -1) {
      events.value[existingEventIndex] = newEvent
    } else {
      events.value.push(newEvent)
    }
  }

  const removeEvent = (date) => {
    const eventIndex = events.value.findIndex(event => event.start === date)
    if (eventIndex !== -1) {
      events.value.splice(eventIndex, 1)
    }
  }

  const addCalendarEvent = (event) => {
    events.value.push(event)
  }
  const signUp = function (payload) {
    const { username, password1, password2, email, name } = payload

    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/auth/registration/', // URL 수정
      data: {
        username, 
        password1, 
        password2,
        email,
        name
      }
    })
      .then((res) => {
        console.log('회원가입 성공:', res.data)
        alert('회원가입이 완료되었습니다. 로그인해주세요.')
        router.push({ name: 'login' })
      })
      .catch((err) => {
        console.log('회원가입 실패:', err.response?.data)
        // 에러 메시지 표시
        if (err.response?.data) {
          const errorMessages = []
          Object.keys(err.response.data).forEach(key => {
            errorMessages.push(`${key}: ${err.response.data[key].join(' ')}`)
          })
          alert(errorMessages.join('\n'))
        } else {
          alert('회원가입 중 오류가 발생했습니다.')
        }
      })
  }

  const logIn = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/auth/login/',
      data: {
        username, password
      }
    })
      .then((res) => {
        // 토큰 저장
        console.log(res.data)
        token.value = res.data.key
        // 토큰을 사용하여 사용자 정보 요청
        return axios({
          method: 'get',
          url: `http://127.0.0.1:8000/api/auth/user/`,
          headers: {
            Authorization: `Token ${res.data.key}`
          }
        })
      })
      .then((userRes) => {
        // 사용자 정보 저장
        const userId = userRes.data.pk
        console.log('User ID:', userId)
        
        // userKey에 pk 저장
        userKey.value = userId
        
        // store에 사용자 정보 저장
        currentUser.value = userRes.data
        
        // 해당 사용자의 캘린더 페이지로 이동
        router.push({ 
          name: 'calender', 
          params: { id: userId }
        })
      })
      .catch((err) => {
        console.log(err)
        alert('로그인에 실패했습니다.')
      })
  }
  const logOut = async () => {
    try {
      await axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/auth/logout/',
        headers: {
          Authorization: `Token ${token.value}`
        }
      })

      sessionStorage.clear()
      token.value = null
      currentUser.value = null
      router.push('/')
    } catch (error) {
      console.error('로그아웃 실패:', error)
      sessionStorage.clear()
      token.value = null
      currentUser.value = null
      router.push('/')
    }
  }
 

 
 
  
  return {userKey,currentUser,logOut, API_URL,signUp,logIn,fowllers,token,events,addCalendarEvent,addOrUpdateEvent,removeEvent}
}, {persist : {
  storage: sessionStorage
}})
