function Login(){
    return (
        <form action="login" method="post">
        <input type="text" placeholder="Username" name="username" />
         <input type="password" placeholder="Password" name="password" />
        <input  type="submit" value="Login" />
      </form>
    )
}
export default Login