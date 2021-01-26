import React from 'react';

export const TalkToConvoPage = () => {

    const submitText = () => {
        fetch(`http://localhost:8080/debug/train`)
        .then(res => res.text())
        .then(res => console.log(res));
    };

    return (
        <div>
            <h2>Talk to Convo</h2>
            <div class="textbox">
                <input type="text" id="textbox" placeholder="Type here..."/>
                <button type="button" onclick={submitText()} id="btn-textbox">Enter</button>
            </div>
        </div>
    )
}
