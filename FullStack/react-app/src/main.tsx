import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "bootstrap/dist/css/bootstrap.css";
import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";
import { BrowserRouter, Route, Routes } from "react-router";
import CharacterList from "./components/CharacterList.tsx";
const client = new ApolloClient({
  uri: "http://localhost:8000/graphql",
  cache: new InMemoryCache(),
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <ApolloProvider client={client}>
        <Routes>
          <Route path="/" element={<CharacterList />}></Route>
        </Routes>
      </ApolloProvider>
    </BrowserRouter>
  </StrictMode>
);
