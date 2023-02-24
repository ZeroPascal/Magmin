import {createSlice, PayloadAction} from '@reduxjs/toolkit'

export enum SocketActions{
    'CONNECTED' = 'CONNECTED',
    'CONNECTING' = 'CONNECTING',
    'DISCONNECTED' = 'DISCONNECTED'
}

export type socketAction = keyof typeof SocketActions;

export interface SocketState{
    socketStatus: socketAction,
    socketConnected: boolean,
    socketID: string
}

const initialState:SocketState={
    socketStatus: SocketActions.DISCONNECTED,
    socketConnected: false,
    socketID: ''
}

const socketSlice= createSlice({
    name: 'socket',
    initialState,
    reducers:{
        setSocketStatus(state, action:PayloadAction<socketAction>){
            state.socketStatus= action.payload
            if(action.payload === SocketActions.CONNECTED){
                state.socketConnected = true
            } else{
                state.socketConnected = false
            }
        },
        setSocketID(state,action:PayloadAction<string>){
            state.socketID = action.payload
        }
    }
})

export const {setSocketStatus, setSocketID} = socketSlice.actions
export default socketSlice.reducer