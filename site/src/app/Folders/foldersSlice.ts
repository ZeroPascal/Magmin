import {createSlice, PayloadAction} from '@reduxjs/toolkit'

export enum FolderActions{
    'ADD_DIRECTORY' = 'ADD_DIRECTORY'
}

export type folderAction = keyof typeof FolderActions

export type Folder={
    root: string,
    name: string,
    recursive: boolean,
    lastScan: number
}
export interface FolderState{
    directories: Folder[]
}

const initialState:FolderState={
    directories: []
}

const folderSlice= createSlice({
    name: 'folder',
    initialState,
    reducers:{
        addFolder(state,action:PayloadAction<Folder>){
            if(action.payload)
                state.directories.push(action.payload)
        },
        setFolders(state,action:PayloadAction<Folder[]>){
            if(action.payload)
            state.directories = action.payload
        }
    }
})

export const {addFolder,setFolders} = folderSlice.actions
export default folderSlice.reducer