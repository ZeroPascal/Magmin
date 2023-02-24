import { RootState } from "../store";

const getState=(state:RootState)=>{
    return state.socketSlice
}

export const socket_status =(state:RootState)=>{
    return getState(state).socketStatus
}

export const socket_connected = (state:RootState)=>{
    return getState(state).socketConnected
}