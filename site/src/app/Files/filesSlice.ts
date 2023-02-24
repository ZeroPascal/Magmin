import { createSlice, PayloadAction } from "@reduxjs/toolkit"

export type File={
    root :string,
    path :string,
    name : string,
    lastAction: string,
    st_ino :number,
    st_atime : number,
    st_atime_ns : number,
    st_birthtime: number,
    st_blksize: number,
    st_blocks: number,
    st_ctime: number,
    st_ctime_ns: number,
    st_mode: number,
    st_mtime:number,
    st_mtime_ns: number,
    st_nlink : number,
    st_rdev : number,
    st_size : number,
    st_dev : number,
    st_flags: number,
    st_gen : number,
    st_gid : number,
    st_uid: number

}

export interface FilesState{
    files:File[]
}
const initialState : FilesState={
    files:[]
}

const filesSlice=createSlice({
    name: 'files',
    initialState,
    reducers:{
        setFiles(state,action:PayloadAction<File[]>){
            state.files = action.payload
        }
    }
})
export const{setFiles} =filesSlice.actions
export default filesSlice.reducer