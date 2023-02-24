import socketIOClinet from 'socket.io-client'
import React, { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { RootState } from "../store"
import { socket_connected} from "./socketSelectors"
import { setSocketStatus, SocketActions } from "./socketSlice"
import socketListeners from './socketListeners'
//import socketListeners from './socketListeners'
export let socket = socketIOClinet( )
export default function Socket() {
  const state = useSelector((state: RootState) => state)
  const socketConnected = socket_connected(state)
  const d = useDispatch()
  
  useEffect(() => {
    if (!socketConnected) {
      try {
        
        socketListeners(socket,d)
        d(setSocketStatus(SocketActions.CONNECTING))

        socket.on('connect', () => {
          d(setSocketStatus(SocketActions.CONNECTED))
        })
        socket.on('disconnect', () => {
          d(setSocketStatus(SocketActions.DISCONNECTED))
       
        })

      } catch (e) {

      }
    }
    return function cleanup() {
     
    }

  }, [d,socketConnected])

  return (<></>)
}