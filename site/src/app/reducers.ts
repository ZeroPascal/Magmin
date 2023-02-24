import {combineReducers} from 'redux'
import socketSlice from './Socket/socketSlice';
import foldersSlice from './Folders/foldersSlice';
import filesSlice from './Files/filesSlice';
const rootReducer = combineReducers({socketSlice,foldersSlice,filesSlice})

export default rootReducer;