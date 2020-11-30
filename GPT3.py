


import os
import openai


def gpt(desp):
        openai.api_key = 'sk-3OC9AX5PDageMzNBhLkMgUAIMRU4R60yZuk0hIrc'

        start_sequence = "\ncode: "
        restart_sequence = "\n\ndescription :"
        preset = """description:  a red button that says stop
        code:  <button style={{color:  'white', backgroundColor: 'red' }}>Stop</button>
        
        description:a anchor tag named Google leading to 'https://www.google.com'
        code:<div className='App'>
            <a href='https://www.google.com/%27%3E'> Google</a>
        </div>

        description:a button for every colour of rainbow
        code: 
        <div>
            <button style={{backgroundColor:'Red'}}>Red</button>
            <button style={{backgroundColor:'Orange'}}>Orange</button>
            <button style={{backgroundColor:'Yellow'}}>Yellow</button>
            <button style={{backgroundColor:'Green'}}>Green</button>
            <button style={{backgroundColor:'Blue'}}>Blue</button>
            <button style={{backgroundColor:'Indigo'}}>Indigo</button>
            <button style={{backgroundColor:'Violet'}}>Violet</button>
        </div>

        description: a sign up page which contains  firstname,lastname,email address and password block with sign up button with already registered redirecting link.
        code:
        <form>
            <h3>Sign Up</h3>
            <div className="form-group">
                <label>First name</label>
                <input type="text" className="form-control" placeholder="First name" />
            </div>
            <div className="form-group">
                <label>Last name</label>
                <input type="text" className="form-control" placeholder="Last name" />
            </div>
            <div className="form-group">
                <label>Email address</label>
                <input type="email" className="form-control" placeholder="Enter email" />
            </div>
            <div className="form-group">
                <label>Password</label>
                <input type="password" className="form-control" placeholder="Enter password" />
            </div>
            <button type="submit" className="btn btn-primary btn-block">Sign Up</button>
            <p className="forgot-password text-right">
                Already registered <a href="#">sign in?</a>
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
    
