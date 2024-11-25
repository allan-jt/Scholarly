import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const [api1, setApi1] = useState("")
  const [api2, setApi2] = useState("")

  useEffect(() => {
    axios.get('http://localhost:8000/').then((res) => {
      console.log(res.data)
      setApi1(res.data)
    })
    axios.get('http://localhost:8000/hello/allan').then((res) => {
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
