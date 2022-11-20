#include <boost/asio.hpp>
#include <boost/asio/experimental/coro.hpp>
#include <iostream>

namespace asio = boost::asio;

using boost::asio::ip::tcp;

boost::asio::experimental::coro<std::string> reader(tcp::socket& sock)
{
  std::string buf;
  while (sock.is_open())
  {
    std::size_t n = co_await boost::asio::async_read_until(
        sock, boost::asio::dynamic_buffer(buf), '\n',
        boost::asio::experimental::use_coro);
    co_yield buf.substr(0, n);
    buf.erase(0, n);
  }
}

boost::asio::awaitable<void> consumer(tcp::socket sock)
{
  auto r = reader(sock);
  auto msg1 = co_await r.async_resume(boost::asio::use_awaitable);
  std::cout << "Message 1: " << msg1.value_or("\n");
  auto msg2 = co_await r.async_resume(boost::asio::use_awaitable);
  std::cout << "Message 2: " << msg2.value_or("\n");
}

boost::asio::awaitable<void> listen(tcp::acceptor& acceptor)
{
  for (;;)
  {
    co_spawn(
        acceptor.get_executor(),
        consumer(co_await acceptor.async_accept(boost::asio::use_awaitable)),
        boost::asio::detached);
  }
}

int main()
{
  boost::asio::io_context ctx;
  tcp::acceptor acceptor(ctx, {tcp::v4(), 54321});
  co_spawn(ctx, listen(acceptor), boost::asio::detached);
  asio::stream_file sf(ctx, "async_resume.cpp", boost::asio::file_base::read_only | boost::asio::file_base::exclusive);
  ctx.run();



}
