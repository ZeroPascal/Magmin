import { RootState } from "../store"

const getState=(state:RootState)=>{
    return state.foldersSlice
}

export const getFolders=(state:RootState)=>{
    return getState(state).directories
}