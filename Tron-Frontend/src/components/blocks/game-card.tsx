"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useCart } from "../contexts/cart-context";

// interface Game {
//   id: number;
//   title: string;
//   image: {
//     src: string;
//   };
//   price: number;
//   genre: string;
//   nftRewards: string[];
//   tags: string[];
// }

interface GameCardProps {
  game: Game;
}

export function GameCard({ game }: GameCardProps) {
  const { addToCart, cart } = useCart();

  return (
    <Card key={game.id}>
      <CardHeader>
        <a href={"/games/" + game.id}>
          <CardTitle>{game.title}</CardTitle>
        </a>
      </CardHeader>
      <CardContent>
        <div className="aspect-w-16 aspect-h-9 w-full overflow-hidden rounded-lg bg-muted mb-4">
          <img
            src={game.images?.[0] ?? "/placeholder.jpg"}
            alt={game.title}
            className="h-full w-full object-cover object-center"
          />
        </div>
        <div className="flex justify-between items-center mb-2">
          <p className="text-2xl font-bold text-primary">
            $TRX {game.price.toFixed(2)}
          </p>
          <Badge variant="secondary">{game.genre}</Badge>
        </div>
        <div className="mt-4">
          <h4 className="font-semibold mb-2">NFT Rewards:</h4>
          <ul className="list-disc list-inside">
            {game.nftRewards?.map((reward, index) => (
              <li key={index} className="text-sm text-muted-foreground">
                {reward.name}
              </li>
            ))}
          </ul>
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {game.tags.map((tag, index) => (
            <Badge key={index} variant="outline">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>
      <CardFooter>
        <Button
          className="w-full"
          onClick={() =>
            cart.some((item) => item.id === game.id)
              ? alert("Item already in cart")
              : addToCart({
                  id: game.id,
                  title: game.title,
                  price: game.price,
                  quantity: 1,
                  developer_wallet_address: game.developerData.wallet_address,
                })
          }
        >
          Add to Cart
        </Button>
      </CardFooter>
    </Card>
  );
}
