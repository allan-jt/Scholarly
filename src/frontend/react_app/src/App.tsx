import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const [api1, setApi1] = useState("")
  const [api2, setApi2] = useState("")
  const api = import.meta.env.VITE_BACKEND_URL

  useEffect(() => {
    axios.get(api).then((res) => {
      console.log(res.data)
      setApi1(res.data)
    })
    axios.get(api + "/hello1/ALlan").then((res) => {
      setApi2(res.data)
    })
  }, [])

  return (
    <>
      <h1>{api1}</h1>
      <h1>{api2}</h1>
    </>
  )
}

export default App
