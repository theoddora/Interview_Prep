import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "bootstrap/dist/css/bootstrap.css";
import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";
import { BrowserRouter, Route, Routes } from "react-router";
import CharacterList from "./components/CharacterList.tsx";
import Character from "./components/Character.tsx";
import Search from "./components/Search.tsx";

const client = new ApolloClient({
  uri: "https://rickandmortyapi.com/graphql",
  cache: new InMemoryCache(),
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <ApolloProvider client={client}>
        <Routes>
          <Route path="/" element={<CharacterList />}></Route>
          <Route path="/search" element={<Search />}></Route>
          <Route path="/:id" element={<Character />}></Route>
        </Routes>
      </ApolloProvider>
    </BrowserRouter>
  </StrictMode>
);
