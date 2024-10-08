"use client";
import { notFound } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { StarIcon, ShoppingCartIcon } from "lucide-react";
import GameImageGallery from "@/components/blocks/game-image-gallery";
import ReviewList from "@/components/blocks/review-list";
import SystemRequirements from "@/components/blocks/system-requirements";
import NavBar from "@/components/ui/navbar";
// import { PLACEHOLDER_GAMES } from "@/components/assets/placeholder-database";
import Footer from "@/components/ui/footer";
import { useGameProducts } from "@/components/contexts/developer-game-products-context";

// This would typically come from an API or database
// const games: { [key: string]: Game } = {
//   "crypto-legends": {
//     id: "crypto-legends",
//     title: "Crypto Legends",
//     price: 19.99,
//     genre: "RPG",
//     description:
//       "Embark on an epic journey through a blockchain-powered world where your actions shape the destiny of the realm. Collect rare NFTs, battle fearsome creatures, and trade with other players in this groundbreaking play-to-earn RPG.",
//     nftRewards: [
//       {
//         name: "Legendary Sword",
//         description: "A powerful weapon forged in the fires of the blockchain.",
//       },
//       {
//         name: "Dragon Egg",
//         description: "A rare item that hatches into a loyal dragon companion.",
//       },
//     ],
//     images: [
//       "/placeholder.svg?height=400&width=600",
//       "/placeholder.svg?height=400&width=600",
//       "/placeholder.svg?height=400&width=600",
//       "/placeholder.svg?height=400&width=600",
//     ],
//     rating: 4.5,
//     reviews: [
//       {
//         id: 1,
//         user: "CryptoGamer",
//         avatar: "/placeholder.svg?height=40&width=40",
//         rating: 5,
//         comment: "Amazing game! The NFT rewards are truly unique and valuable.",
//       },
//       {
//         id: 2,
//         user: "BlockchainExplorer",
//         avatar: "/placeholder.svg?height=40&width=40",
//         rating: 4,
//         comment:
//           "Great concept and execution. Can't wait to see how the game evolves.",
//       },
//     ],
//     systemRequirements: {
//       os: "Windows 10 64-bit",
//       processor: "Intel Core i5-6600K or AMD Ryzen 5 1600",
//       memory: "8 GB RAM",
//       graphics: "NVIDIA GeForce GTX 1060 6GB or AMD Radeon RX 580 8GB",
//       storage: "50 GB available space",
//     },
//   },
//   // Add more games here...
// };
export default function GameDetailsPage({
  params,
}: {
  params: { slug: string };
}) {
  const { products, loading } = useGameProducts();
  const games: { [key: string]: Game } = products
    .map((game) => ({
      [game.id]: game,
    }))
    .reduce((acc, game) => ({ ...acc, ...game }), {});
  const game = games[params.slug];
  if (loading) {
    return <div>Loading...</div>;
  }
  if (!game) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-background">
      <NavBar />

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid md:grid-cols-2 gap-8">
          {game.images && (
            <GameImageGallery images={game.images} title={game.title} />
          )}
          <div>
            <h1 className="text-3xl font-bold text-primary mb-2">
              {game.title}
            </h1>
            <div className="flex items-center mb-4">
              <div className="flex mr-2">
                {[...Array(5)].map((_, i) => (
                  <StarIcon
                    key={i}
                    className={`h-5 w-5 ${
                      i < Math.floor(game.rating ?? 0)
                        ? "text-yellow-400 fill-current"
                        : "text-muted-foreground"
                    }`}
                  />
                ))}
              </div>
              <span className="text-muted-foreground">
                {(game.rating ?? 0).toFixed(1)} ({(game.reviews ?? []).length}{" "}
                reviews)
              </span>
            </div>
            <Badge variant="secondary" className="mb-4">
              {game.genre}
            </Badge>
            <p className="text-muted-foreground mb-6">{game.description}</p>
            <div className="flex items-center justify-between mb-6">
              <span className="text-3xl font-bold text-primary">
                ${game.price.toFixed(2)}
              </span>
              <Button className="flex items-center">
                <ShoppingCartIcon className="mr-2 h-4 w-4" />
                Add to Cart
              </Button>
            </div>
            <h2 className="text-xl font-semibold mb-2">NFT Rewards</h2>
            <div className="grid gap-4 mb-6">
              {game.nftRewards?.map((reward, index) => (
                <Card key={index}>
                  <CardHeader>
                    <CardTitle>{reward.name}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">
                      {reward.description}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>

        <Tabs defaultValue="reviews" className="mt-12">
          <TabsList>
            <TabsTrigger value="reviews">Reviews</TabsTrigger>
            <TabsTrigger value="system-requirements">
              System Requirements
            </TabsTrigger>
          </TabsList>
          <TabsContent value="reviews">
            <ReviewList reviews={game.reviews ?? []} />
          </TabsContent>
          <TabsContent value="system-requirements">
            {game.systemRequirements && (
              <SystemRequirements requirements={game.systemRequirements} />
            )}
          </TabsContent>
        </Tabs>
      </main>
      <Footer />
    </div>
  );
}
