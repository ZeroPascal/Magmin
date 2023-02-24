import { RootState } from "../store"

const getState=(state:RootState)=>{
    return state.filesSlice
}

export const getFiles=(state:RootState)=>{
    return getState(state).files
}

export const getFilesFromFolder=(state:RootState, folderRoot:string)=>{
    return getFiles(state).filter(file=>{
        return file.root === folderRoot
    })
}