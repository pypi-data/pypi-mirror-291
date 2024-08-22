<p align="center" style="margin: 0 0 0px">
  <img width="281" height="237" src="https://trove.fm/images/sesh_logo_medium.png" alt='Sesh'>
</p>

<div align="center">
    <h1 align="center" style="font-size: 3rem; margin: -15px 0"></h1>
    <p align="center" style="font-size: 1.2rem; margin: 20px 0"><em>Session Management for FastAPI</em></p>
    <img src="https://gitlab.com/brianfarrell/sesh/badges/main/pipeline.svg?key_text=Test%20Suite">
    <img src="https://gitlab.com/brianfarrell/sesh/badges/main/coverage.svg?key_text=Coverage">
    <img src="https://gitlab.com/brianfarrell/sesh/-/badges/release.svg?key_text=Release">
</div>

## Features

- Secure your FastAPI app with cookies rather than tokens
- Use dependency injection to protect routes and manage state data
- Extensible API supports multiple, custom cookies
- Redis is the first backend to be supported, but several others are in the works
- Use multiple backends simultaneously
- Pydantic models and static typing are used throughout to verify data and ease development
- Abstract Base Classes for Session and SessionStore to ease development of custom tools

## Links

Gitlab Repository: https://gitlab.com/brianfarrell/sesh

Documentation: https://brianfarrell.gitlab.io/sesh/

PyPi Release: https://pypi.org/project/sesh/

License: https://www.gnu.org/licenses/agpl.html
