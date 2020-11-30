


import os
import openai


def gpt(desp):
        openai.api_key = 'sk-3OC9AX5PDageMzNBhLkMgUAIMRU4R60yZuk0hIrc'

        start_sequence = "\ncode: "
        restart_sequence = "\n\ndescription :"
        preset = """description:  a red button that says stop
        code:  <button style="color:  'white', backgroundColor: 'red' ">Stop</button>
        
        description:a anchor tag named Google leading to 'https://www.google.com'
        code:<div className='App'>
            <a href='https://www.google.com/%27%3E'> Google</a>
        </div>

        description:a button for every colour of rainbow
        code: 
        <div>
            <button style="background-color:'red'">Red</button>
            <button style="background-color:'orange'">Orange</button>
            <button style="background-color:'yellow'">Yellow</button>
            <button style="background-color:'green'">Green</button>
            <button style="background-color:'blue'">Blue</button>
            <button style="background-color:'dodgerblue'">Indigo</button>
            <button style="background-color:'purple'">Violet</button>
        </div>

        description: a sign up page which contains  firstname,lastname,email address and password block with sign up button with already registered redirecting link.
        code:
        <form>
            <h2>Sign Up</h2>
            <div class="form-group">
                <label>First name</label>
                <input type="text" class="form-control" placeholder="First name" />
            </div>
            <div class="form-group">
                <label>Last name</label>
                <input type="text" class="form-control" placeholder="Last name" />
            </div>
            <div class="form-group">
                <label>Email address</label>
                <input type="email" class="form-control" placeholder="Enter email"/>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control" placeholder="Enter password"/>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Sign Up</button>
            <p class="forgot-password text-right">
                Already registered <a href="#">Sign in</a>
            </p>
        </form>


        description: """+desp+ "\n\n"

        response = openai.Completion.create(
        engine="davinci",
        prompt=preset,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        stop=["\n\n"]
        )

        return response.choices[0]['text']
    
