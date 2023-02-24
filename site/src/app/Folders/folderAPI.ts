import { Folder } from "./foldersSlice";

export const addDirectory=(folder:Folder):Promise<boolean>=>{
    return new Promise((res,rej)=>{
        res(true)
    })
}