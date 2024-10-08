"use client";
import React, {
  createContext,
  useState,
  ReactNode,
  useEffect,
  useContext,
} from "react";

// Define the context type

interface GameProductsContextType {
  products: Game[];
  addProduct: (product: Game) => void;
  loading: boolean;
}

interface ApiResponse {
  status: string;
  message: string;
  data: {
    games: Game[];
  };
  timestamp: string;
}

// Create the context with default values
const GameProductsContext = createContext<GameProductsContextType | undefined>(
  undefined
);
const FASTAPI_URL = process.env.FASTAPI_URL;

// Create a provider component
export const GameProductsProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [loading, setLoading] = useState(true);
  const [products, setProducts] = useState<Game[]>([
    {
      id: "crypto-legends",
      title: "Crypto Legends",
      price: 19.99,
      genre: "RPG",
      description: "An epic RPG set in the world of blockchain.",
      nftRewards: [
        {
          name: "Legendary Sword",
          description: "A powerful sword with unique abilities.",
        },
        {
          name: "Dragon Egg",
          description: "A rare egg that can hatch into a dragon.",
        },
      ],
      images: ["/placeholder.svg?height=225&width=400"],
      tags: ["Blockchain", "Fantasy", "Multiplayer"],
      rating: 4.5,
      systemRequirements: {
        os: "Windows 10",
        processor: "Intel i5",
        memory: "8 GB RAM",
        graphics: "NVIDIA GTX 970",
        storage: "50 GB available space",
      },
      developerData: {
        name: "Crypto Studios",
        wallet_address: "TRiNL4y9JUatnMF5hh7TipKJGK7m7aWepq",
      },
      game_id: "670529aaabf8c12950d09b82",
      createdAt: "2024-10-08T19:46:34.262000",
      updatedAt: "2024-10-08T19:52:12.612000",
      reviews: [],
    },
  ]);

  const retrieveGameProducts = async () => {
    try {
      const response = await fetch(`${FASTAPI_URL}/v1/games/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      // console.log("Response status:", response.status);
      // console.log("Response headers:", response.headers);
      // console.log("Response body:", await response.json());
      //console.log(response);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result: ApiResponse = await response.json();
      //console.log("Result:", result.data.games);
      setProducts(result.data.games as Game[]);
      //console.log("Products:", products);
      //console.log("Loading:", loading);
    } catch (err) {
      console.error("There was a problem with the fetch operation:", err);
    } finally {
      setLoading(false);
      //console.log("Loading:", loading);
    }
  };
  useEffect(() => {
    retrieveGameProducts();
  }, []);

  const addProduct = (product: Game) => {
    setProducts((prevProducts = []) => [...prevProducts, product]);
  };

  return (
    <GameProductsContext.Provider value={{ products, addProduct, loading }}>
      {children}
    </GameProductsContext.Provider>
  );
};

// Export the context and provider
export const useGameProducts = () => {
  const context = useContext(GameProductsContext);
  if (context === undefined) {
    throw new Error(
      "useGameProducts must be used within a GameProductsProvider"
    );
  }
  return context;
};
