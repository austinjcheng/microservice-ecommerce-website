import express, { Request, Response } from 'express';
import passport from 'passport';
import jwt from 'jsonwebtoken';
import { Strategy as LocalStrategy } from 'passport-local';
import { Strategy as JwtStrategy, ExtractJwt } from 'passport-jwt';

const app = express();
app.use(express.json());

// Set up authentication strategies
passport.use(new LocalStrategy(
  // Specify options for local strategy
  {
    usernameField: 'email',
    passwordField: 'password'
  },
  // Define the authentication function
  (email: string, password: string, done: any) => {
    // TODO: Implement authentication logic here
    // Check if the email and password are valid
    if (email === 'test@example.com' && password === 'password') {
      // If valid, return user object
      return done(null, { id: 1, email: 'test@example.com' });
    } else {
      // If invalid, return false
      return done(null, false);
    }
  }
));

// Set up JWT strategy
passport.use(new JwtStrategy(
  // Specify options for JWT strategy
  {
    jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
    secretOrKey: 'secret'
  },
  // Define the verification function
  (jwtPayload: any, done: any) => {
    // TODO: Implement JWT verification logic here
    // Check if the user exists and the JWT is valid
    if (jwtPayload.sub === 'test@example.com') {
      // If valid, return user object
      return done(null, { id: 1, email: 'test@example.com' });
    } else {
      // If invalid, return false
      return done(null, false);
    }
  }
));

// Define routes
app.post('/login', (req: Request, res: Response) => {
  // Authenticate user using passport-local strategy
  passport.authenticate('local', { session: false }, (err, user) => {
    if (err || !user) {
      // If authentication fails, return error message
      return res.status(401).json({ message: 'Invalid email or password' });
    } else {
      // If authentication succeeds, create JWT and return it
      const token = jwt.sign({ sub: user.email }, 'secret');
      return res.json({ token });
    }
  })(req, res);
});

app.get('/profile', passport.authenticate('jwt', { session: false }), (req: Request, res: Response) => {
  // Return user profile information
  res.json(req.user);
});

// Start server
app.listen(3000, () => {
  console.log('Server started on port 3000');
});
